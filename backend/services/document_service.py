from fastapi import Path
from llama_index.readers.file import PDFReader
import re
import arxiv
import os
from typing import List

from backend.services.embedding_service import EmbeddingService
import logging

logger = logging.getLogger(__name__)

class DocumentService:
    
    
    def __init__(self, embedding_service: EmbeddingService, max_results: int = 50):
        logger.info("Initializing DocumentService")
        self.loader = PDFReader()
        self.arxiv = arxiv.Client()
        self.max_results = max_results
        self.embedding_service = embedding_service

        
    def process_and_embed_papers(self, query: str) -> dict:
        logger.info("Processing papers for query: {query}")

        """
        Fetch papers, process them, and create embeddings.
        
        Args:
            query: Search query for arXiv
            
        Returns:
            Dictionary with processing statistics
        """
        try:
            # Fetch papers
            logger.info(f"Processing papers for query: {query}")

            papers = self.fetch_papers(query)
            if not papers:
                return {"status": "error", "message": "No papers found"}

            # Load and clean documents
            cleaned_docs = self.load_and_clean_documents(papers)

            if not cleaned_docs:
                return {"status": "error", "message": "No documents processed successfully"}

            # Create embeddings and store in vector store
            self.embedding_service.run_pipeline(cleaned_docs)

            return {
                "status": "success",
                "papers_fetched": len(papers),
                "documents_processed": len(cleaned_docs),
                "query": query
            }

        except Exception as e:
            logger.error(f"Error in process_papers: {str(e)}")

            return {
                "status": "error",
                "message": str(e)
            }

    def fetch_papers(self, query: str, sort_by: arxiv.SortCriterion = arxiv.SortCriterion.SubmittedDate) -> List[dict]:
        
        """
        Fetch papers from arxiv based on query.
        """
        # Create search object with parameters
        search = arxiv.Search(
            query=query,
            max_results=self.max_results,
            sort_by=sort_by,
            sort_order=arxiv.SortOrder.Descending
        )

        # Get results
        papers = []
        for result in self.arxiv.results(search):
            paper_info = {
                'title': result.title,
                'published': result.published,
                'authors': [author.name for author in result.authors],
                'arxiv_id': result.get_short_id(),
                'pdf_url': result.pdf_url,
                'abstract': result.summary
            }
            papers.append(paper_info)
            
            logging.debug(paper_info)
            
            # Download PDF
            filename = f"papers/{paper_info['arxiv_id']}.pdf"
            os.makedirs("papers", exist_ok=True)
            try:
                result.download_pdf(filename=filename)
                paper_info['local_path'] = filename
            except Exception as e:
                print(f"Failed to download {paper_info['arxiv_id']}: {str(e)}")
                continue
                
        return papers
    
    def load_and_clean_documents(self, papers: List[dict]) -> List:
        all_documents = []
        
        for paper in papers:
            if 'local_path' not in paper:
                continue
                
            try:
                # Convert string path to Path object safely
                paper_path = Path(paper['local_path'])
                
                # Check if file exists before trying to load it
                if not paper_path.exists():
                    logger.warning(f"File not found: {paper_path}")
                    continue
                    
                # Load PDF
                documents = self.loader.load_data(file=paper_path)
                
                cleaned_docs = []
                for doc in documents:
                    cleaned_text = self.clean_up_text(doc.text)
                    doc.text = cleaned_text
                    # Add metadata
                    doc.metadata.update({
                        'title': paper.get('title', ''),
                        'authors': paper.get('authors', []),
                        'published_date': paper.get('published', ''),
                        'arxiv_id': paper.get('arxiv_id', ''),
                        'abstract': paper.get('abstract', '')
                    })
                    cleaned_docs.append(doc)
                
                all_documents.extend(cleaned_docs)
                
                # Optional: Clean up PDF file after processing
                # paper_path.unlink()  # Uncomment if you want to delete files after processing
                
            except Exception as e:
                logger.error(f"Failed to process {paper.get('arxiv_id', 'unknown')}: {str(e)}")
                continue
                    
        return all_documents
    
    @staticmethod
    def clean_up_text(content: str) -> str:
        """
        Remove unwanted characters and patterns in text input.

        :param content: Text input.
        
        :return: Cleaned version of original text input.
        """

        # Fix hyphenated words broken by newline
        content = re.sub(r'(\w+)-\n(\w+)', r'\1\2', content)

        # Remove specific unwanted patterns and characters
        unwanted_patterns = [
            "\\n", "  —", "——————————", "—————————", "—————",
            r'\\u[\dA-Fa-f]{4}', r'\uf075', r'\uf0b7'
        ]
        for pattern in unwanted_patterns:
            content = re.sub(pattern, "", content)

        # Fix improperly spaced hyphenated words and normalize whitespace
        content = re.sub(r'(\w)\s*-\s*(\w)', r'\1-\2', content)
        content = re.sub(r'\s+', ' ', content)

        return content
    
    
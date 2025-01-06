from pathlib import Path  
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
        logger.info(f"Processing papers for query: {query}")

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
        logging.info(f"Fetching papers for this query {query}")

        # Create search object with parameters
        search = arxiv.Search(
            query=query,
            max_results=self.max_results,
            sort_by=sort_by,
            sort_order=arxiv.SortOrder.Descending
        )

        papers_dir = "backend/papers"
        os.makedirs(papers_dir, exist_ok=True)
            # Get results
        papers = []
        logging.info("Iterating through arxiv results")
        for result in self.arxiv.results(search):
            paper_info = {
                'title': result.title,
                'published': result.published,
                'authors': [author.name for author in result.authors],
                'arxiv_id': result.get_short_id(),
                'pdf_url': result.pdf_url,
                'abstract': result.summary
            }
            logging.debug(paper_info)
            papers.append(paper_info)
            
            
            # Download PDF
            filename = os.path.join(papers_dir, f"{paper_info['arxiv_id']}.pdf")
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
                logger.warning(f"Skipping paper without local_path: {paper.get('arxiv_id', 'unknown')}")
                continue
                
            try:
                paper_path = Path(paper['local_path'])
                
                if not paper_path.exists():
                    logger.warning(f"File not found: {paper_path}")
                    continue
                    
                # Load PDF
                logger.info(f"Loading PDF: {paper_path}")
                documents = self.loader.load_data(file=paper_path)
                logger.info(f"Loaded {len(documents)} document segments from {paper_path}")
                
                cleaned_docs = []
                for idx, doc in enumerate(documents):
                    try:
                        # Clean text
                        original_length = len(doc.text)
                        cleaned_text = self.clean_up_text(doc.text)
                        cleaned_length = len(cleaned_text)
                        
                        logger.debug(f"Document {idx}: Cleaned text length {original_length} -> {cleaned_length}")
                        
                        if not cleaned_text.strip():
                            logger.warning(f"Skipping empty document after cleaning: {paper_path} segment {idx}")
                            continue
                            
                        doc.text = cleaned_text
                        
                        # Add metadata
                        doc.metadata.update({
                            'title': paper.get('title', ''),
                            'authors': paper.get('authors', []),
                            'published_date': paper.get('published', ''),
                            'arxiv_id': paper.get('arxiv_id', ''),
                            'abstract': paper.get('abstract', ''),
                            'segment_id': idx
                        })
                        
                        cleaned_docs.append(doc)
                        
                    except Exception as e:
                        logger.error(f"Error cleaning document segment {idx} from {paper_path}: {str(e)}")
                        continue
                        
                logger.info(f"Successfully cleaned {len(cleaned_docs)} segments from {paper_path}")
                all_documents.extend(cleaned_docs)
                
            except Exception as e:
                logger.error(f"Failed to process {paper.get('arxiv_id', 'unknown')}: {str(e)}")
                continue
                    
        logger.info(f"Total documents processed: {len(all_documents)}")
        return all_documents
        
    @staticmethod
    def clean_up_text(content: str) -> str:

        try:
            # Handle surrogate pairs by encoding and decoding with error handling
            content = content.encode('utf-16', 'surrogatepass').decode('utf-16', 'replace')
            
            # Fix hyphenated words broken by newline
            content = re.sub(r'(\w+)-\n(\w+)', r'\1\2', content)

            # Remove specific unwanted patterns and characters
            unwanted_patterns = [
                r"\\n",                    # Escaped newlines
                r"\s*—\s*",               # Em dashes with optional spaces
                r"—{3,}",                 # Multiple em dashes
                r"\\u[\dA-Fa-f]{4}",      # Unicode escapes
                r"[\uf075\uf0b7]",        # Specific Unicode characters
                r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]",  # Control characters
                r"[^\x00-\x7F]+",         # Non-ASCII characters
            ]
            
            for pattern in unwanted_patterns:
                content = re.sub(pattern, " ", content)

            # Fix spacing issues
            content = re.sub(r'(\w)\s*-\s*(\w)', r'\1-\2', content)  # Fix hyphenation
            content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
            
            # Final cleanup of any remaining problematic characters
            content = ''.join(char for char in content if ord(char) < 0x10000)
            
            return content.strip()
        except Exception as e:
            logger.error(f"Error in clean_up_text: {str(e)}")
            # Return a safe version of the text if cleaning fails
            return ''.join(char for char in content if ord(char) < 128).strip()
        
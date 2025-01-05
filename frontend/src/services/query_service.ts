import {
    GeneralSearchResponse,
    MedicalSearchParams,
    NutritionSearchParams,
    QueryGeneralRequest,
    SearchResponse,
} from "@/utils/types";
import axios, { AxiosError } from "axios";

const API_BASE_URL = "http://localhost:8000/api/query";

export class QueryService {
    private static instance: QueryService;

    private constructor() {}

    public static getInstance(): QueryService {
        if (!QueryService.instance) {
            QueryService.instance = new QueryService();
        }
        return QueryService.instance;
    }

    private handleError(error: unknown) {
        if (error instanceof AxiosError) {
            throw new Error(
                error.response?.data?.detail || "An error occurred",
            );
        }
        throw error;
    }

    // General query endpoint
    public async searchGeneral(
        input: QueryGeneralRequest,
    ): Promise<GeneralSearchResponse> {
        try {
            const response = await axios.post<GeneralSearchResponse>(
                `${API_BASE_URL}/general`,
                input,
            );
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    // Nutrition search endpoint
    public async searchNutrition(
        params: NutritionSearchParams,
    ): Promise<Record<string, any>> {
        try {
            const { query, dietary_restrictions, allergies } = params;
            const queryParams = new URLSearchParams();

            if (dietary_restrictions) {
                dietary_restrictions.forEach((restriction) =>
                    queryParams.append("dietary_restrictions", restriction)
                );
            }

            if (allergies) {
                allergies.forEach((allergy) =>
                    queryParams.append("allergies", allergy)
                );
            }

            const response = await axios.post<Record<string, any>>(
                `${API_BASE_URL}/nutrition?${queryParams.toString()}`,
                { query },
            );
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    // Medical information search endpoint
    public async searchMedical(
        params: MedicalSearchParams,
    ): Promise<Record<string, any>> {
        try {
            const { query, include_research = false, credentials } = params;
            const response = await axios.post<Record<string, any>>(
                `${API_BASE_URL}/medical`,
                {
                    query,
                    include_research,
                    credentials,
                },
            );
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }

    // Ask health question endpoint
    public async askHealthQuestion(
        query: string,
    ): Promise<Record<string, any>> {
        try {
            const response = await axios.post<Record<string, any>>(
                `${API_BASE_URL}/ask`,
                { query },
            );
            return response.data;
        } catch (error) {
            this.handleError(error);
            throw error;
        }
    }
}

// Export a singleton instance
export const queryService = QueryService.getInstance();

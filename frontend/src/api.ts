export interface Question {
  category?: string;
  question: string;
}

export interface GenerateQuestionsResponse {
  questions: Question[];
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error("VITE_API_BASE_URL is not defined in the environment variables.");
}

export async function generateQuestions(jobTitle: string): Promise<Question[]> {
  const response = await fetch(`${API_BASE_URL}/questions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ job_title: jobTitle }),
  });

  if (!response.ok) {
    throw new Error('Failed to generate questions. Please try again later.');
  }

  const data: GenerateQuestionsResponse = await response.json();
  return data.questions;
}

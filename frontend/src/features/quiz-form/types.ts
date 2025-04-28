export interface Option {
  A: string;
  B: string;
  C: string;
  D: string;
}

export interface Question {
  question: string;
  options: Option;
  answer: string;
  explanation: string;
}

export interface Quiz {
  questions: Question[];
}

export interface ErrorResponse {
  status: number;
  message: string;
}

export interface QuizResponse {
  id: string;
  preview: Quiz;
  difficultyValue: string;
}

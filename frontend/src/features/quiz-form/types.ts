export interface Option {
  A: string;
  B: string;
  C: string;
  D: string;
}

export interface Question {
  content: string;
  options: Option;
  answer: string;
  explanation: string;
}

export interface Quiz {
  questions: Question[];
}

export interface QuizResponse {
  id: string;
  preview: Quiz;
}

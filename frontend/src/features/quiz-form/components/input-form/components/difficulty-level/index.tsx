import React from "react";
import { Difficulty } from "@/features/quiz-form/components/input-form/types";

interface Props {
  difficulty: Difficulty;
  setDifficulty: React.Dispatch<React.SetStateAction<Difficulty>>;
  isSubmitting: boolean;
}

export const DifficultyLevel: React.FC<Props> = ({
  difficulty,
  setDifficulty,
  isSubmitting,
}) => {
  return (
    <div>
      <label className="flex justify-start mb-2 font-medium">
        <span className="mr-1">⚡️</span>
        <p className="font-bold">難易度</p>
      </label>
      <select
        value={difficulty}
        onChange={(e) => setDifficulty(e.target.value as Difficulty)}
        className={`w-full p-2 border border-emerald-300 rounded ${
          isSubmitting ? "cursor-not-allowed" : ""
        }`}
        required
        disabled={isSubmitting}
      >
        <option value={Difficulty.BEGINNER}>かんたん 📚</option>
        <option value={Difficulty.INTERMEDIATE}>ふつう 🧠</option>
        <option value={Difficulty.ADVANCED}>むずかしい 🚀</option>
      </select>
    </div>
  );
};

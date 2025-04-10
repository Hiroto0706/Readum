import React from "react";
import { Difficulty } from "@/features/quiz-form/components/input-form/types";
import { DifficultyMessage } from "@/features/quiz-form/components/input-form/components/difficulty-level/types";

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
        <option value={Difficulty.BEGINNER}>
          {DifficultyMessage.beginner.value}
        </option>
        <option value={Difficulty.INTERMEDIATE}>
          {DifficultyMessage.intermediate.value}
        </option>
        <option value={Difficulty.ADVANCED}>
          {DifficultyMessage.advanced.value}
        </option>
      </select>

      <div>
        <button
          type="button"
          onClick={() => setDifficulty(Difficulty.BEGINNER)}
          className={`font-bold text-white rounded-full my-3 py-1 px-3 w-[calc(33%-8px)] box-border text-xs md:text-base  duration-300 mr-2 ${
            DifficultyMessage.beginner.style
          } ${
            isSubmitting
              ? "cursor-not-allowed"
              : `cursor-pointer ${DifficultyMessage.beginner.hovered}`
          }`}
          disabled={isSubmitting}
        >
          {DifficultyMessage.beginner.value}
        </button>
        <button
          type="button"
          onClick={() => setDifficulty(Difficulty.INTERMEDIATE)}
          className={`font-bold text-white rounded-full my-3 py-1 px-3 w-[calc(33%-8px)] box-border text-xs md:text-base duration-300 mx-2 ${
            DifficultyMessage.intermediate.style
          } ${
            isSubmitting
              ? "cursor-not-allowed"
              : `cursor-pointer ${DifficultyMessage.intermediate.hovered}`
          }`}
          disabled={isSubmitting}
        >
          {DifficultyMessage.intermediate.value}
        </button>
        <button
          type="button"
          onClick={() => setDifficulty(Difficulty.ADVANCED)}
          className={`font-bold text-white rounded-full my-3 py-1 px-3 w-[calc(33%-8px)] box-border text-xs md:text-base  duration-300 ml-2 ${
            DifficultyMessage.advanced.style
          } ${
            isSubmitting
              ? "cursor-not-allowed"
              : `cursor-pointer ${DifficultyMessage.advanced.hovered}`
          }`}
          disabled={isSubmitting}
        >
          {DifficultyMessage.advanced.value}
        </button>
      </div>
    </div>
  );
};

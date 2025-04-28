import Image from "next/image";
import React from "react";

interface Props {
  isSubmitting: boolean;
}

export const SubmitButton: React.FC<Props> = ({ isSubmitting }) => {
  return (
    <>
      <button
        type="submit"
        disabled={isSubmitting}
        className={`w-full flex justify-center bg-emerald-500 text-white font-medium py-2 px-4 mb-4 rounded disabled:opacity-50 duration-300 ${
          isSubmitting
            ? "cursor-not-allowed"
            : "hover:bg-emerald-600 cursor-pointer"
        }`}
      >
        {!isSubmitting && (
          <Image
            src="/icons/generate.svg"
            alt="Generate icon"
            width={20}
            height={20}
            className="mr-2"
          />
        )}
        <p className="flex items-center">
          {isSubmitting ? (
            <>
              クイズの作成中...
              <span
                className="ml-2 inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"
                aria-label="読み込み中"
              />
            </>
          ) : (
            "クイズを作成する！"
          )}
        </p>
      </button>
      {isSubmitting && (
        <span className="text-sm text-gray-500 mb-4 block">
          クイズの作成には1~3分程度かかります
        </span>
      )}
    </>
  );
};

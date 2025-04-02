import Image from "next/image";
import React from "react";

interface Props {
  isSubmitting: boolean;
}

export const SubmitButton: React.FC<Props> = ({ isSubmitting }) => {
  return (
    <button
      type="submit"
      disabled={isSubmitting}
      className={`w-full flex justify-center bg-emerald-500 text-white font-medium py-2 px-4 rounded disabled:opacity-50 duration-300 ${
        isSubmitting
          ? "cursor-not-allowed"
          : "hover:bg-emerald-600 cursor-pointer"
      }`}
    >
      <Image
        src="/icons/generate.svg"
        alt="Generate icon"
        width={20}
        height={20}
        className="mr-2"
      />
      <p>{isSubmitting ? "作成中..." : "クイズを作成する！"}</p>
    </button>
  );
};

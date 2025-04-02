import React from "react";

interface Props {
  error: string;
}

export const ErrorMessage: React.FC<Props> = ({ error }) => {
  return (
    <>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}
    </>
  );
};

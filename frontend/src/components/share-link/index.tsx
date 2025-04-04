"use client";

import Image from "next/image";
import React from "react";

export default function ShareButton() {
  const handleShare = async () => {
    try {
      // 現在のURLをコピー
      await navigator.clipboard.writeText(window.location.href);

      alert("URLのコピーの成功しました");
    } catch (error) {
      console.error("URLのコピーに失敗しました:", error);
      alert("URLのコピーに失敗しました。");
    }
  };

  return (
    <div className="flex justify-center items-center">
      <button
        onClick={handleShare}
        className="bg-emerald-500 hover:bg-emerald-600 text-white font-medium py-2 px-6 rounded-full mb-8 flex justify-center items-center cursor-pointer duration-300 shadow-md"
      >
        <Image
          src="/icons/share.svg"
          alt="Share icon"
          width={20}
          height={20}
          className="mr-2"
        />
        Share
      </button>
    </div>
  );
}

"use client";

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
    <button
      onClick={handleShare}
      className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded"
    >
      シェア用のリンクを作成する
    </button>
  );
}

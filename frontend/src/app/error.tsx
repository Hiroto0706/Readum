"use client";

import Link from "next/link";

export default function Page({ error }: { error: Error }) {
  return (
    <div className="text-center py-48">
      <h1 className="text-2xl font-bold">500エラー</h1>
      <p className="pt-8 pb-4">予期せぬエラーが発生しました。</p>

      <p className="text-start font-bold mb-2 text-red-500">
        エラーメッセージ：
      </p>
      <div className="border border-red-500 rounded bg-red-50 mb-6 p-4 font-bold text-red-500">
        {error.message}
      </div>

      <Link href="/" className="text-blue-500">
        トップページに戻る
      </Link>
    </div>
  );
}

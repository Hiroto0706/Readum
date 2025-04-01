import React from "react";

export const Description: React.FC = () => {
  return (
    <>
      {/* mt-16はHeader分の高さ */}
      <section className="mt-16 py-2 md:py-8">
        <div className="text-left my-4 md:my-8 max-w-[800px] mx-auto px-2">
          <div className="mb-2 md:flex md:items-baseline">
            <h2 className="text-7xl font-bold text-emerald-500 inline-block">
              Readum
            </h2>
            <p className="text-2xl inline-block font-bold md:ml-2">
              であなたの読書を可視化しよう！
            </p>
          </div>
          <p className="text-gray-600 max-w-2xl text-sm">
            Readumは生成AIテクノロジーを活用したクイズ生成アプリケーションです。
            <br></br>
            あなたの読書メモや学習内容をフォームに入力して送信するだけで、AIが自動的にあなたの理解度を測るためのオリジナルクイズを作成してくれます。
          </p>
        </div>
      </section>
    </>
  );
};

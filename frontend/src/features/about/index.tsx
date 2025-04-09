import Image from "next/image";
import Link from "next/link";
import React from "react";

export const About: React.FC = () => {
  return (
    <div className="px-2">
      <h1 className="flex items-center text-2xl font-bold py-8">
        <Image
          src="/icons/star.svg"
          alt="Star icon"
          width={32}
          height={32}
          className="mr-2"
        />
        About Readum
      </h1>

      <p className="mb-8">
        Readumは生成AIを用いた学習体験を向上させるためのツールです。<br></br>
        使い方は非常に簡単です。入力フォームにあなたの読書メモを貼り付けて、クイズを生成するだけです。
        <br></br>
        <br></br>
        クイズに答えることで、正答率が表示され、
        <span className="font-bold">あなたの読書に対する理解度が可視化</span>
        されます。
        <br></br>
        ぜひ100点を獲得し、読書マスターを目指してください！
      </p>

      <div className="mb-8">
        <div className="p-4 bg-emerald-50 rounded-lg mb-6">
          <h2 className="text-xl font-semibold mb-2">
            <span className="mr-2">⚡️</span>
            使い方
          </h2>
          <p className="mb-2">
            当アプリケーションは先進技術を活用して、あなたの読書ノートを分析し、考えさせられるクイズ問題を作成します。
          </p>
        </div>
        <ol className="list-none pl-0 mb-6 space-y-4 font-bold">
          <li className="flex items-start">
            <span className="flex items-center justify-center bg-emerald-500 text-white rounded-full w-8 h-8 mr-3 flex-shrink-0 font-bold">
              1
            </span>
            <span className="pt-1">
              読書のメモまたはコンテンツのURLを入力する
            </span>
          </li>
          <li className="flex items-start">
            <span className="flex items-center justify-center bg-emerald-500 text-white rounded-full w-8 h-8 mr-3 flex-shrink-0 font-bold">
              2
            </span>
            <span className="pt-1">難易度と問題数を選択</span>
          </li>
          <li className="flex items-start">
            <span className="flex items-center justify-center bg-emerald-500 text-white rounded-full w-8 h-8 mr-3 flex-shrink-0 font-bold">
              3
            </span>
            <span className="pt-1">選択形式の問題に答えて知識をテスト</span>
          </li>
          <li className="flex items-start">
            <span className="flex items-center justify-center bg-emerald-500 text-white rounded-full w-8 h-8 mr-3 flex-shrink-0 font-bold">
              4
            </span>
            <span className="pt-1">役立つ解説付きの結果を確認</span>
          </li>
          <li className="flex items-start">
            <span className="flex items-center justify-center bg-emerald-500 text-white rounded-full w-8 h-8 mr-3 flex-shrink-0 font-bold">
              5
            </span>
            <span className="pt-1">
              シェアボタンをクリックして、クイズの結果をシェアしよう
            </span>
          </li>
        </ol>
      </div>

      <div className="mb-16">
        <div className="p-4 bg-emerald-50 rounded-lg mb-6">
          <h2 className="text-xl font-semibold mb-2">
            <span className="mr-2">⚡️</span>
            お問い合わせ
          </h2>
          <p className="mb-2">
            Readumに関することならなんでも承っています。
            <br></br>
            バグ、ご意見、ご提案なんでもお待ちしています！
          </p>
        </div>

        <p>
          <Link
            href="https://forms.gle/W952dNLQBio7Nkpt9"
            className="text-blue-500"
            target="_blank"
            rel="noopener noreferrer"
          >
            こちら
          </Link>
          よりお問い合わせください。
        </p>
      </div>
    </div>
  );
};

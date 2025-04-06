import Link from "next/link";

export default function Page() {
  return (
    <div className="text-center py-48">
      <h1 className="text-2xl font-bold">404エラー</h1>
      <p className="py-8">
        指定されたページが見つかりませんでした。
        <br></br>
        別のURLで再度お試しください。
      </p>

      <Link href="/" className="text-blue-500">
        トップページに戻る
      </Link>
    </div>
  );
}

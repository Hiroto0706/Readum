import type { Metadata } from "next";
import "@/styles/globals.css";
import { Header } from "@/components/header";
import { Footer } from "@/components/footer";

export const metadata: Metadata = {
  title: "Readum",
  description: "Readumはあなたの読書を可視化するAIテストアプリケーションです",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="max-w-[800px] mx-auto">
        <Header />

        <main className="text-emerald-900 mt-16">{children}</main>

        <Footer />
      </body>
    </html>
  );
}

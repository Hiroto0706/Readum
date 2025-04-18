import type { Metadata } from "next";
import "@/styles/globals.css";
import { Header } from "@/components/header";
import { Footer } from "@/components/footer";
import { headers } from "next/headers";

export async function generateMetadata(): Promise<Metadata> {
  const host = (await headers()).get("host");
  const protocol = process.env.NODE_ENV === "production" ? "https" : "http";
  const baseURL = `${protocol}://${host}`;

  return {
    metadataBase: new URL(baseURL),
    title: "Readum",
    description: "Readumはあなたの読書を可視化するAIテストアプリケーションです",
  };
}

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

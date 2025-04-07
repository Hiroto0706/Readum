import { Result } from "@/features/result";
import { UserAnswer } from "@/features/result/types";
import { notFound } from "next/navigation";
import React from "react";

async function fetchResult(uuid: string) {
  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_SERVER_SIDE_URL}/result/${uuid}`
    );

    if (!response.ok) {
      if (response.status === 404) {
        return notFound();
      }
      throw new Error(`Failed to fetch result: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching result:", error);
    throw error;
  }
}

interface Props {
  params: Promise<{ uuid: string }>;
}

export default async function Page({ params }: Props) {
  const { uuid } = await params;
  const result: UserAnswer = await fetchResult(uuid);

  return <Result result={result} />;
}

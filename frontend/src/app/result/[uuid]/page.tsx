import { Result } from "@/features/result";
import { UserAnswer } from "@/features/result/types";
import { BASE_URL } from "@/config";
import { notFound } from "next/navigation";
import React, { cache } from "react";

const fetchResult = cache(async (uuid: string): Promise<UserAnswer> => {
  try {
    const response = await fetch(`${BASE_URL}/result/${uuid}`);

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
});

interface Props {
  params: Promise<{ uuid: string }>;
}

export default async function Page({ params }: Props) {
  const { uuid } = await params;
  const result: UserAnswer = await fetchResult(uuid);

  return <Result result={result} />;
}

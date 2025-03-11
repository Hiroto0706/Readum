export default async function Page() {
  const res = await fetch(
    process.env.NEXT_PUBLIC_BASE_URL + "/quiz/create_quiz",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        type: "text",
        content: "this is a test content.",
        difficulty: "intermediate",
        questionCount: 10,
      }),
    }
  );
  const payload = await res.json();
  const quiz_content = payload.preview;

  console.log(quiz_content);

  return (
    <>
      Hello World.<br></br>
      {quiz_content.questions.map((quiz: any, index: number) => (
        <div key={index}>
          quizContent: {quiz.content}
          <br></br>
          quizOptions: <br></br>
          A: {quiz.options.A}
          <br></br>
          B: {quiz.options.B}
          <br></br>
          C: {quiz.options.C}
          <br></br>
          D: {quiz.options.D}
          <br></br>
          answer: {quiz.answer}
          <br></br>
          explanation: {quiz.explanation}
          <br></br>
          -----------
          <br></br>
        </div>
      ))}
    </>
  );
}

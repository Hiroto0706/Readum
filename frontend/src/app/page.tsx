export default async function Page() {
  const res = await fetch("http://localhost:8000/api/v1/create_question", {
    method: "POST",
  });
  const payload = await res.json();
  const message = payload.message;

  return (
    <>
      Hello World.<br></br>
      this is a message from FastAPI → {message}
    </>
  );
}

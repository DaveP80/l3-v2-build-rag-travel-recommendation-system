import type { MetaFunction } from "@remix-run/node";
import { exec } from "child_process";
import Travel from "~/components/Travel";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to travel recommendations!" },
  ];
};

export const action = async ({ request }: {request: Request}) => {
  const formData = await request.formData();
  let input = formData.get('prompt') as string;

  const res = new Promise((resolve, reject) => {
    exec(`python3 trip.py "${input}"`, (error, stdout, stderr) => {
      if (error) {
        reject({ error: stderr });
      }
      resolve({message: stdout})
    });
  });

  return {newResponse: await res}
};

export default function Index() {

  return (
    <div className="flex h-screen items-center justify-center">
      <div className="flex flex-col items-center gap-10">
        <header className="flex flex-col items-center gap-7">
          <h1 className="leading text-2xl font-bold text-gray-800 dark:text-gray-100">
            Welcome to <span className="">Travel Recommendation, OpenAI planner!</span>
          </h1>
        </header>
        <Travel/>
      </div>
    </div>
  );
}


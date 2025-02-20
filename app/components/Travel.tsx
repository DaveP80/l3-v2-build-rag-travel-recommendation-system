import { Form, useActionData, useSubmit } from "@remix-run/react";
import { useEffect, useState } from "react";
import { makePrompt } from "~/utils/helper";

// Example component using fetch to call the API
function Travel() {
  const ChatAction = useActionData();
  const submit = useSubmit()
  const [isLoading, setLoading] = useState(false); // To handle loading state
  const handleSubmit = async (args: (EventTarget & HTMLFormElement)[]) => {
    setLoading(true); // Start loading
    const input = makePrompt(args);
    if (!input) return;
    submit({ prompt: input }, { method: "post" });
  };

  useEffect(() => {
    if (ChatAction?.newResponse) {
      setLoading(false)
    }

  }, [ChatAction])

  let stdRes = isLoading ? null : ChatAction?.newResponse ? ChatAction.newResponse?.message || ChatAction.newResponse?.error : null;

  return (
    <>
      <Form className="flex flex-col space-y-4" onSubmit={(e) => {
        e.preventDefault()
        handleSubmit([e.currentTarget.gender.value, e.currentTarget.age.value, e.currentTarget.education.value, e.currentTarget.general_area.value,
          e.currentTarget.pets.value, e.currentTarget.environment.value.toString()
        ]);
      }}>
        <label htmlFor="gender">Enter your gender:</label>
        <input name="gender" type="textarea" placeholder="male / female" className="border border-gray-300 rounded-md p-2" />
        <label htmlFor="age">Enter your age:</label>
        <input name="age" type="textarea" placeholder="21" className="border border-gray-300 rounded-md p-2" />
        <label htmlFor="education">Enter your education level:</label>
        <input name="education" type="textarea" placeholder="high school" className="border border-gray-300 rounded-md p-2" required />
        <label htmlFor="general_area">Enter your general location:</label>
        <input name="general_area" type="textarea" placeholder="london, england" className="border border-gray-300 rounded-md p-2" required />
        <label htmlFor="pets">Enter your pets if any:</label>
        <input name="pets" type="textarea" placeholder="e.g. 1 dog, 2 fish" className="border border-gray-300 rounded-md p-2" required />
        <div className="form-control">
  <label className="label cursor-pointer" htmlFor="environment">
    <span className="label-text">Is the environment a concern?</span>
    <input type="checkbox" name="environment" defaultChecked className="checkbox checkbox-primary" />
  </label>
</div>
        <button type="submit" className="bg-green-500 text-white py-2 rounded-md">Submit your personal information prompt</button>
      </Form>
      {isLoading ? <div className="flex justify-center items-center">
        <div className="spinner"></div>{" "}
      </div> : ChatAction?.newResponse ? <p>{stdRes}</p> : null}

    </>
  );
}

export default Travel;
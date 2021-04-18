import { useState } from "preact/hooks";
import { File } from "./directory-listing";

interface Props {
  file: File;
}

export default function EditSidebar({ file }: Props) {
  const [isLoading, setLoading] = useState(false);
  const [name, setName] = useState(file.name);

  const submitChange = async (e: Event) => {
    e.preventDefault();
    console.log({ name });
    setLoading(true);
    await fetch("POSTYOLODATA");
    // ...
    //setLoading(false);
  };

  return (
    <div className="w-80 bg-red-500">
      <h1>{file.name}</h1>
      <p>{isLoading && 'Bitte Warten sie!'}</p>
      <form onSubmit={submitChange}>
        {name}
        <input
          type="text"
          value={name}
          onInput={(e) => setName((e.target as HTMLInputElement).value)}
        />
        <input type="submit" disabled={isLoading} />
      </form>
    </div>
  );
}

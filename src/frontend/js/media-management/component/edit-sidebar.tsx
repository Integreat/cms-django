import { Trash2 } from "preact-feather";
import { useEffect, useState } from "preact/hooks";
import { getCsrfToken } from "../../utils/csrf-token";
import { File } from "./directory-listing";

interface Props {
  file: File;
  editMediaEndpoint: string;
  deleteMediaEndpoint: string;
  finishEditSidebar: () => any;
  selectionMode?: boolean;
  globalEdit?: boolean;
  selectMedia?: (file: File) => any;
}

export default function EditSidebar({
  file,
  editMediaEndpoint,
  deleteMediaEndpoint,
  finishEditSidebar,
  selectionMode,
  selectMedia,
  globalEdit
}: Props) {
  const [isLoading, setLoading] = useState(false);
  const [changed_file, setChanged_file] = useState(file);
  const [success, setSuccess] = useState(false);
  useEffect(() => {
    setChanged_file(file);
    setSuccess(false);
  }, [file]);

  const submitChange = async (e: Event) => {
    e.preventDefault();
    setLoading(true);
    try {
      const change_call = await fetch(editMediaEndpoint, {
        method: "POST",
        mode: "same-origin",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify(changed_file),
      });
      const server_response = await change_call.json();
      if (server_response.success) {
        setSuccess(true);
      }
      finishEditSidebar();
    } catch (error) {
      console.log(error);
    }

    setLoading(false);
  };

  const deleteFile = async (e: Event) => {
    e.preventDefault();
    setLoading(true);

    try {
      const change_call = await fetch(deleteMediaEndpoint, {
        method: "POST",
        mode: "same-origin",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify(changed_file),
      });
      const server_response = await change_call.json();
      if (server_response.success) {
        setSuccess(true);
      }
      finishEditSidebar();
    } catch (error) {
      console.log(error);
    }

    setLoading(false);
  };

  return (
    <div className="w-1/3 rounded-lg border-blue-500 shadow bg-white min-h-full m-0">
      <div class="h-30 items-center max-w-full">
        <img src={file.thumbnailPath} class="max-w-60 m-2 mx-auto"></img>
        {success && <div>Erfolg</div>}
      </div>
      <form onSubmit={submitChange} encType="multipart/form-data" method="post">
        <div class="p-4 border-b">
          <h2 class="font-bold cursor-pointer">Dateiname:</h2>
          <input
            type="text"
            disabled={selectionMode || (!globalEdit && file.isGlobal)}
            value={changed_file.name}
            onInput={(e) =>
              setChanged_file({
                ...changed_file,
                name: (e.target as HTMLInputElement).value,
              })
            }
            class="appearance-none block w-full bg-gray-200 text-xl text-gray-800 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-400"
          />
        </div>
        <div>
          <div class="md:grid md:grid-cols-2 hover:bg-gray-50 md:space-y-0 space-y-1 p-4 border-b">
            <p class="text-gray-600">Dateityp:</p>
            <p>{file.file_type}</p>
          </div>
          <div class="md:grid md:grid-cols-2 hover:bg-gray-50 md:space-y-0 space-y-1 p-4 border-b">
            <p class="text-gray-600">Hochgeladen am:</p>
            <p>{file.uploadedAt}</p>
          </div>
          <div class="p-4 border-b">
            <h2 class="font-bold cursor-pointer">Alternativer Text:</h2>
            <input
              type="text"
              value={changed_file.alt_text}
              disabled={selectionMode || (!globalEdit && file.isGlobal)}
              onInput={(e) =>
                setChanged_file({
                  ...changed_file,
                  alt_text: (e.target as HTMLInputElement).value,
                })
              }
              class="appearance-none block w-full bg-gray-200 text-xl text-gray-800 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-400"
            />
          </div>
        </div>
        {!selectionMode &&  (globalEdit || !file.isGlobal) && (
          <div class="p-4">
            <button
              title="Speichern"
              class="confirmation-button w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 mb-2 rounded"
              type="submit"
            >
              Aktualisieren
            </button>
            <button
              title="Datei löschen"
              class="confirmation-button w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
              onClick={deleteFile}
            >
              <Trash2 class="mr-2 inline-block h-4" />
              Datei löschen
            </button>
          </div>
        )}
        {selectionMode && (
          <div class="p-4">
            <button
              title="Auswählen"
              onClick={(e) => {
                e.preventDefault();
                if (selectMedia) {
                  selectMedia(file);
                }
              }}
              class="confirmation-button w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 mb-2 rounded"
              type="submit"
            >
              Auswählen
            </button>
          </div>
        )}
      </form>
    </div>
  );
}

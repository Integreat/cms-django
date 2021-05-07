import { render } from "preact";
import { XCircle } from "preact-feather";
import MediaManagement from ".";
import { File } from "./component/directory-listing";

interface Props {
  cancel: () => any;
  selectMedia: (file: File) => any;
}

export default function SelectMedia({ cancel, selectMedia }: Props) {
  return (
    <div className="flex flex-col items-center justify-center w-full h-full fixed inset-0 z-50 m-auto" style="z-index: 2000;">
      <div className="w-10/12 h-5/6 flex flex-col justify-center relative">
        <div class="h-full content bg-gray-200 w-full p-4 shadow-md rounded">
          <MediaManagement
            selectionMode
            selectMedia={selectMedia}
            apiEndpoints={{
              getDirectoryContent: "/ajax/nurnberg/media/directory_content",
              editMediaUrl: "/ajax/nurnberg/media_edit",
              createDirectory: "/ajax/nurnberg/media_edit/create_directory",
              uploadFile: "/ajax/nurnberg/media_edit/upload_file",
              deleteMediaUrl: "/ajax/nurnberg/media_edit/delete_file",
              getDirectoryPath: "/ajax/nurnberg/media_edit/directory_path",
            }}
          ></MediaManagement>
        </div>
        <button onClick={cancel} className="absolute top-6 right-3">
          <XCircle className="inline-block h-8 w-8" />
        </button>
      </div>
    </div>
  );
}

(window as any).IntegreatSelectMediaDialog = SelectMedia;
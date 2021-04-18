import { render } from "preact";
import { useState } from "preact/hooks";
import Button from "./component/button";
import DirectoryListing, { File } from "./component/directory-listing";
import EditSidebar from "./component/edit-sidebar";

export interface MediaApiPaths {
  getDirectoryContent: string;
}

interface Props {
  apiEndpoints: MediaApiPaths;
}

const MediaManagement = (props: Props) => {
  const [parentDirectory, setParentDirectory] = useState<number | null>(null);
  const [editFile, setEditFile] = useState<File|null>(null);

  return (
    <div>
      <div className="flex flex-wrap items-center">
        <h2 className="heading font-normal mb-2 p-2">Medienbibliothek</h2>
        <div className="flex-1"></div>
        <div className="flex flex-wrap justify-start">
          <Button label="Verzeichnis erstellen" />
          <Button label="Datei hochladen" />
        </div>
      </div>
      <div className="flex items-stretch">
        <div className="flex-1">
          <DirectoryListing
            parentDirectory={parentDirectory}
            apiEndpoints={props.apiEndpoints}
            setDirectory={setParentDirectory}
            setEditFile={setEditFile}
          ></DirectoryListing>
        </div>
        {editFile && <EditSidebar file={editFile}></EditSidebar>}
      </div>
    </div>
  );
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("integreat-media-management").forEach((el) => {
    const apiEndpoints = {
      getDirectoryContent: el.getAttribute("data-get-directory-content"),
    };
    render(<MediaManagement apiEndpoints={apiEndpoints} />, el);
  });
});

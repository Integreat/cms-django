import { render } from "preact";
import { useState } from "preact/hooks";
import { MediaApiPaths } from ".";
import Button from "./component/button";
import DirectoryListing, { File } from "./component/directory-listing";
import EditSidebar from "./component/edit-sidebar";

interface Props {
  apiEndpoints: MediaApiPaths;
  parentDirectory?: number | null;
  path?: string;
  default?: true;
}

export default function Listing(props: Props) {
  const [editFile, setEditFile] = useState<File | null>(null);

  return (
    <div>
      <div className="flex flex-wrap items-center">
        <h2 className="heading font-normal mb-2 p-2">Medienbibliothek</h2>
        <div className="flex-1"></div>
        <div className="flex flex-wrap justify-start">
          <Button
            href={`/create_directory/${props.parentDirectory || 0}`}
            label="Verzeichnis erstellen"
          />
          <Button
            href={`/upload_file/${props.parentDirectory || 0}`}
            label="Datei hochladen"
          />
        </div>
      </div>
      <div className="flex items-stretch">
        <div className="flex-1" onClick={() => setEditFile(null)}>
          <DirectoryListing
            parentDirectory={props.parentDirectory}
            apiEndpoints={props.apiEndpoints}
            setEditFile={setEditFile}
          ></DirectoryListing>
        </div>
        {editFile && (
          <EditSidebar
            file={editFile}
            editMediaEndpoint={props.apiEndpoints.editMediaUrl}
          ></EditSidebar>
        )}
      </div>
    </div>
  );
}

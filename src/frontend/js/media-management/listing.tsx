import { render } from "preact";
import { useEffect, useState } from "preact/hooks";
import { MediaApiPaths } from ".";
import MediacenterBreadcrumb from "./component/breadcrumb";
import Button from "./component/button";
import DirectoryListing, { Directory, File } from "./component/directory-listing";
import EditSidebar from "./component/edit-sidebar";

interface Props {
  apiEndpoints: MediaApiPaths;
  parentDirectory?: number | null;
  path?: string;
  default?: true;
  selectionMode?: boolean;
  selectMedia?: (file: File) => any;
  globalEdit?: boolean;
}

export default function Listing(props: Props) {
  const [editFile, setEditFile] = useState<File | null>(null);
  const [refreshCounter, setRefreshCounter] = useState(0);

  const [directory, setDirectory] = useState<Directory | null>(null);

  useEffect(() => {
    if (props.parentDirectory) {
      (async () => {
        try {
          let url = props.apiEndpoints.getDirectoryPath;
          url += "?directory=" + props.parentDirectory;

          const result = await fetch(url);
          const data = await result.json();

          setDirectory(data.data[data.data.length - 1]);
        } catch (e) {
          console.error(e);
        }
      })();
    } else {
      setDirectory(null);
    }
  }, [props.parentDirectory]);

  return (
    <div className="max-h-full flex flex-col">
      <div className="flex flex-wrap items-center">
        <h2 className="heading font-normal mb-2 p-2">Medienbibliothek</h2>
        <div className="flex-1"></div>
        {!props.selectionMode && (props.globalEdit || !directory?.isGlobal) && (
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
        )}
      </div>
      <MediacenterBreadcrumb directoryId={props.parentDirectory} apiEndpoints={props.apiEndpoints} />
      <div className="flex flex-1 overflow-auto items-stretch">
        <div className="flex-1" onClick={() => setEditFile(null)}>
          <DirectoryListing
            parentDirectory={props.parentDirectory}
            apiEndpoints={props.apiEndpoints}
            setEditFile={setEditFile}
            refresh={refreshCounter}
          ></DirectoryListing>
        </div>
        {editFile && (
          <EditSidebar
            file={editFile}
            editMediaEndpoint={props.apiEndpoints.editMediaUrl}
            deleteMediaEndpoint={props.apiEndpoints.deleteMediaUrl}
            finishEditSidebar={() => {
              setEditFile(null);
              setRefreshCounter(refreshCounter + 1);
            }}
            selectionMode={props.selectionMode}
            selectMedia={props.selectMedia}
            globalEdit={props.globalEdit}
          ></EditSidebar>
        )}
      </div>
    </div>
  );
}

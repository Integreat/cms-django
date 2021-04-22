import { useEffect, useState } from "preact/hooks";
import { MediaApiPaths } from "..";
import DirectoryEntry from "./directory-entry";
import FileEntry from "./file-entry";

interface Props {
  parentDirectory: number | null;
  apiEndpoints: MediaApiPaths;
  setDirectory: (directoryId: number) => void;
  setEditFile: (file: File)=>void;
}

export interface File {
  id: number;
  name: string;
  path: string;
  alt_text: string;
  file_type: string;
  thumbnailPath?: string;
  uploadedAt: Date;
  type: "file";
}

export interface Directory {
  id: number;
  name: string;
  numberOfEntries: number;
  type: "directory";
}

type MediaLibraryEntry = File | Directory;

export default function DirectoryListing({
  parentDirectory,
  apiEndpoints,
  setDirectory,
  setEditFile,
}: Props) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState<MediaLibraryEntry[]>([]);

  useEffect(() => {
    console.log(parentDirectory);
    (async () => {
      setItems([]);
      setIsLoaded(false);
      try {
        let url = apiEndpoints.getDirectoryContent;
        if(parentDirectory) {
          url += '?directory=' + parentDirectory;
        }
        const result = await fetch(url);
        const data = await result.json();
        if (!data.success) {
          setError(true);
        }
        setItems(data.data);
      } catch (e) {
        console.error(e);
        setError(true);
      }
      setIsLoaded(true);
    })();
  }, [parentDirectory]);

  return (
    <div className="grid grid-cols-gallery">
      {items.map((item) =>
        item.type === "directory" ? (
          <DirectoryEntry item={item} onClick={(e) => {e.stopPropagation(); setDirectory(item.id)}} />
        ) : (
          <FileEntry item={item} onClick={(e) => {e.stopPropagation(); setEditFile(item)}} />
        )
      )}
    </div>
  );
}

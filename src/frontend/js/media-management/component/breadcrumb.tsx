import { Link } from "preact-router";
import { useEffect, useState } from "preact/hooks";
import { MediaApiPaths } from "..";
import { Directory } from "./directory-listing";

interface Props {
  directoryId: number;
  apiEndpoints: MediaApiPaths;
}

export default function MediacenterBreadcrumb({
  directoryId,
  apiEndpoints,
}: Props) {
  const [breadCrumbs, setBreadcrumbs] = useState<Directory[]>([]);

  useEffect(() => {
    if (directoryId) {
      (async () => {
        try {
          let url = apiEndpoints.getDirectoryPath;
          url += "?directory=" + directoryId;

          const result = await fetch(url);
          const data = await result.json();

          setBreadcrumbs(data.data);
        } catch (e) {
          console.error(e);
        }
      })();
    } else {
        setBreadcrumbs([]);
    }
  }, [directoryId]);

  return (
    <nav>
      <ul class="px-2 flex flex-wrap gap-2">
        <li>
          <Link href={`/`}>Root</Link>
        </li>
        {breadCrumbs.map((directory, i) => (
          <>
            <li>/</li>
            <li>
              <Link href={`/listing/${directory.id}`}>{directory.name}</Link>
            </li>
          </>
        ))}
      </ul>
    </nav>
  );
}

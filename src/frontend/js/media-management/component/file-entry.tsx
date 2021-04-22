import { File as FileIcon } from "preact-feather";
import { File } from "./directory-listing";

interface Props {
  item: File;
  onClick: (event: MouseEvent) => void

}
export default function FileEntry({ item, onClick }: Props) {
  return (
    <div className="flex flex-col items-center h-44 cursor-pointer" onClick={onClick}>
      {item.thumbnailPath ? (
        <img className="h-full w-3/4 object-cover" src={item.thumbnailPath} />
      ) : (
        <FileIcon className="w-full h-24" />
      )}
      <div className="flex-1"></div>
      <span class="align-baseline">{item.name}</span>
    </div>
  );
}

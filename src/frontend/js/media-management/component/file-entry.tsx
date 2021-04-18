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
        <img className="h-24" src={item.thumbnailPath} />
      ) : (
        <FileIcon className="w-full h-24" />
      )}
      <div className="flex-1"></div>
      <span>{item.name}</span>
      <span>&nbsp;</span>
    </div>
  );
}

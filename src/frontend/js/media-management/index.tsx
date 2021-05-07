import { render, h } from "preact";
import Router from "preact-router";
import { createHashHistory } from "history";
import Listing from "./listing";
import CreateDirectory from "./create-directory";
import UploadFile from "./upload-file";
import { File } from "./component/directory-listing";
export interface MediaApiPaths {
  getDirectoryContent: string;
  editMediaUrl: string;
  createDirectory: string;
  uploadFile: string;
  deleteMediaUrl: string;
  getDirectoryPath: string;
}

interface Props {
  apiEndpoints: MediaApiPaths;
  selectionMode?: boolean;
  selectMedia?: (file: File) => any;
  globalEdit?: boolean;
}

export default function MediaManagement(props: Props) {
  return (
    <Router history={createHashHistory() as any}>
      <Listing path="" {...props} />
      <Listing path="/listing/:parentDirectory" {...props} />
      {!props.selectionMode && (
        <CreateDirectory path="/create_directory/:parentDirectory" {...props} />
      )}
      {!props.selectionMode && (
        <UploadFile path="/upload_file/:parentDirectory" {...props} />
      )}
    </Router>
  );
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("integreat-media-management").forEach((el) => {
    const apiEndpoints = {
      getDirectoryContent: el.getAttribute("data-get-directory-content"),
      editMediaUrl: el.getAttribute("data-edit-media-url"),
      createDirectory: el.getAttribute("data-create-directory-url"),
      uploadFile: el.getAttribute("data-upload-file-url"),
      deleteMediaUrl: el.getAttribute("data-delete-file-url"),
      getDirectoryPath: el.getAttribute("data-directory-path-url"),
    };
    render(<MediaManagement apiEndpoints={apiEndpoints} globalEdit={el.hasAttribute('data-enable-global-edit')} />, el);
  });
});

(window as any).IntegreatMediaManagement = MediaManagement;
(window as any).preactRender = render;
(window as any).preactJSX = h;

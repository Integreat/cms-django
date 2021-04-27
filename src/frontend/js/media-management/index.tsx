import { render } from "preact";
import Router from "preact-router";
import { createHashHistory } from "history";
import Listing from "./listing";
import CreateDirectory from "./create-directory";
import UploadFile from "./upload-file";
export interface MediaApiPaths {
  getDirectoryContent: string;
  editMediaUrl: string;
  createDirectory: string;
  uploadFile: string;
}

interface Props {
  apiEndpoints: MediaApiPaths;
}

const MediaManagement = (props: Props) => {
  return (
    <Router history={createHashHistory() as any}>
      <Listing path="" {...props} />
      <Listing path="/listing/:parentDirectory" {...props} />
      <CreateDirectory path="/create_directory/:parentDirectory" {...props} />
      <UploadFile path="/upload_file/:parentDirectory" {...props} />
    </Router>
  );
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("integreat-media-management").forEach((el) => {
    const apiEndpoints = {
      getDirectoryContent: el.getAttribute("data-get-directory-content"),
      editMediaUrl: el.getAttribute("data-edit-media-url"),
      createDirectory: el.getAttribute("data-create-directory-url"),
      uploadFile: el.getAttribute("data-upload-file-url"),
    };
    render(<MediaManagement apiEndpoints={apiEndpoints} />, el);
  });
});

import { useEffect, useMemo, useState } from "react";

import {
  X,
  ZoomIn,
  ZoomOut,
  Expand,
  Download,
} from "lucide-react";

import {
  Document,
  Page,
  pdfjs,
} from "react-pdf";

import type { DocumentSource } from "../types/DocumentSource";

import { useLayout } from "../../../components/layouts/AppShell/useLayout";

import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";


pdfjs.GlobalWorkerOptions.workerSrc =
  new URL(
    "pdfjs-dist/build/pdf.worker.min.mjs",
    import.meta.url,
  ).toString();


interface Props {
  source: DocumentSource | null;
}


function SourceViewer({
  source,
}: Props) {

  const {
    previewVisible,
    setPreviewVisible,
  } = useLayout();


  const [numPages, setNumPages] =
    useState(0);

  const [cacheKey, setCacheKey] =
    useState("");

  const [scale, setScale] =
    useState(1.1);


  useEffect(() => {
    setNumPages(0);
    setScale(1.1);

    setCacheKey(
      crypto.randomUUID(),
    );

  }, [source]);


  const pdfUrl = useMemo(() => {

    if (!source?.document_url) {
      return null;
    }


    let url =
      source.document_url;


    if (!url.startsWith("http")) {

      const apiUrl =
        import.meta.env.VITE_API_URL ??
        "http://localhost:8000";


      url =
        `${apiUrl}${url}`;
    }


    return `${url}?v=${cacheKey}`;

  }, [source, cacheKey]);



  function zoomIn() {

    setScale((value) =>
      Math.min(
        value + 0.15,
        3,
      ),
    );
  }


  function zoomOut() {

    setScale((value) =>
      Math.max(
        value - 0.15,
        0.6,
      ),
    );
  }


  function fitView() {

    setScale(1.1);

  }



  function openPdf() {

    if (pdfUrl) {

      window.open(
        pdfUrl,
        "_blank",
        "noopener,noreferrer",
      );

    }
  }



  function downloadPdf() {

    if (!pdfUrl) return;


    const link =
      document.createElement("a");


    link.href = pdfUrl;


    link.download =
      source?.document_name ??
      "document.pdf";


    link.click();

  }



  if (!previewVisible) {
    return null;
  }



  return (

    <>

      {/* Overlay */}

      <div
        className="
          fixed
          inset-0
          z-40

          bg-black/40
          backdrop-blur-sm
        "
        onClick={() =>
          setPreviewVisible(false)
        }
      />


      {/* Drawer */}

      <aside

        className="
          fixed
          inset-y-0
          right-0
          z-50

          flex
          h-full
          w-full
          flex-col

          bg-white

          border-l
          border-slate-200

          shadow-2xl

          animate-in
          slide-in-from-right
          duration-300

          md:w-[90vw]
          lg:w-[80vw]
          xl:w-[75vw]
        "

      >


        {/* Header */}

        <div
          className="
            sticky
            top-0
            z-10

            flex
            h-14
            shrink-0

            items-center
            justify-between

            border-b
            border-slate-200

            bg-white

            px-5
          "
        >

          <h2
            className="
              text-sm
              font-semibold
              text-slate-800
            "
          >
            Document Preview
          </h2>



          <div
            className="
              flex
              items-center
              gap-1
            "
          >

            <button
              onClick={zoomOut}
              className="
                rounded-lg
                p-2
                hover:bg-slate-100
              "
            >
              <ZoomOut size={18}/>
            </button>



            <span
              className="
                w-14
                text-center

                text-xs
                font-medium
                text-slate-500
              "
            >
              {Math.round(scale * 100)}%
            </span>



            <button
              onClick={zoomIn}
              className="
                rounded-lg
                p-2
                hover:bg-slate-100
              "
            >
              <ZoomIn size={18}/>
            </button>



            <button
              onClick={fitView}
              className="
                rounded-lg
                px-2
                py-1

                text-xs
                font-medium

                hover:bg-slate-100
              "
            >
              Fit
            </button>



            <button
              onClick={openPdf}
              className="
                rounded-lg
                p-2
                hover:bg-slate-100
              "
              title="Open PDF"
            >
              <Expand size={18}/>
            </button>



            <button
              onClick={downloadPdf}
              className="
                rounded-lg
                p-2
                hover:bg-slate-100
              "
              title="Download"
            >
              <Download size={18}/>
            </button>



            <button
              onClick={() =>
                setPreviewVisible(false)
              }
              className="
                rounded-lg
                p-2

                text-slate-500

                hover:bg-slate-100
              "
            >
              <X size={18}/>
            </button>


          </div>

        </div>




        {!source ? (

          <div
            className="
              flex
              flex-1

              items-center
              justify-center

              text-sm
              text-slate-500
            "
          >
            Select a source
          </div>


        ) : (

          <>


            {/* Metadata */}

            <div
              className="
                shrink-0

                border-b
                border-slate-200

                px-5
                py-3
              "
            >

              <p
                className="
                  truncate

                  text-sm
                  font-semibold

                  text-slate-900
                "
              >
                {source.document_name}
              </p>


              <p
                className="
                  mt-1

                  text-xs

                  text-slate-500
                "
              >
                Page {source.page}
                {" • "}
                Chunk {source.chunk_index}
              </p>


            </div>




            {/* PDF Viewer */}


            <div
              className="
                flex-1

                overflow-auto

                bg-slate-100

                p-8
              "
            >


              {!pdfUrl ? (

                <p
                  className="
                    text-center
                    text-sm
                    text-red-500
                  "
                >
                  PDF URL unavailable
                </p>


              ) : (


                <Document

                  key={pdfUrl}

                  file={pdfUrl}

                  loading={
                    <p
                      className="
                        py-10

                        text-center

                        text-sm
                      "
                    >
                      Loading PDF...
                    </p>
                  }


                  onLoadSuccess={({
                    numPages,
                  }) =>
                    setNumPages(numPages)
                  }

                >

                  <div
                    className="
                      flex
                      min-w-max

                      justify-center
                    "
                  >

                    <Page

                      pageNumber={
                        source.page
                      }

                      scale={scale}

                      renderAnnotationLayer

                      renderTextLayer

                    />

                  </div>


                </Document>

              )}



              {numPages > 0 && (

                <p
                  className="
                    mt-4

                    text-center

                    text-xs

                    text-slate-500
                  "
                >
                  Page {source.page} of{" "}
                  {numPages}
                </p>

              )}


            </div>


          </>

        )}

      </aside>


    </>

  );

}


export default SourceViewer;
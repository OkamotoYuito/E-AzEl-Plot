"use client";

import SettingSidebar from "@/components/SettingSidebar";
import Plot from "@/components/Plot";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { PanelLeftOpen, PanelRightOpen, X } from "lucide-react";

export default function Page() {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

  return (
    <main className="flex h-screen overflow-hidden bg-background">
      {isMobile && (
        <Button
          variant="ghost"
          size="icon"
          className="absolute top-2 left-2 z-20 text-foreground"
          onClick={toggleSidebar}
        >
          {isSidebarOpen ? (
            <X className="h-5 w-5" />
          ) : (
            <PanelRightOpen className="h-5 w-5" />
          )}
        </Button>
      )}
      <div
        className={`transition-all duration-300 ease-in-out overflow-y-auto border-r bg-card text-card-foreground
                    ${
                      isSidebarOpen
                        ? "w-full sm:w-[clamp(240px,25vw,300px)]"
                        : "w-0"
                    }
                    ${isMobile && !isSidebarOpen ? "hidden" : "flex flex-col"}
                    ${
                      isMobile && isSidebarOpen
                        ? "absolute h-full z-10 shadow-lg"
                        : ""
                    }`}
      >
        <SettingSidebar onPlot={(url) => setImageUrl(url)} />
      </div>
      <div className="flex-1 flex flex-col relative">
        {!isMobile && (
          <Button
            variant="outline"
            size="icon"
            className="absolute top-2 left-2 z-10"
            onClick={toggleSidebar}
          >
            {isSidebarOpen ? (
              <PanelLeftOpen className="h-5 w-5" />
            ) : (
              <PanelRightOpen className="h-5 w-5" />
            )}
          </Button>
        )}
        <Plot imageUrl={imageUrl} />
      </div>
    </main>
  );
}

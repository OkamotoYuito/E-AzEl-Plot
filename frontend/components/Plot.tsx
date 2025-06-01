"use client";

import Image from "next/image";

interface PlotProps {
  imageUrl: string | null;
}

export default function Plot({ imageUrl }: PlotProps) {
  if (!imageUrl) return null;

  return (
    <div className="p-4 flex-1 h-full flex justify-center items-center overflow-hidden">
      <Image
        src={imageUrl}
        alt="AzEl Plot"
        className="max-w-full max-h-full object-contain border border-gray-300 rounded"
      />
    </div>
  );
}

"use client";

import { useEffect, useState } from "react";
import ObservationSettings from "./settings/ObservationSettings";
import TargetList from "./settings/TargetList";
import AddTargetForm from "./settings/AddTargetForm";
import { toast } from "sonner";

interface Target {
  name: string;
  color: string;
}

interface TargetNameError {
  name: string;
  error: string;
}

interface SettingSidebarProps {
  onPlot: (url: string) => void;
}

const INITIAL_TARGETS: Target[] = [{ name: "Sun", color: "#dc143c" }];
const COLOR_PALETTE = [
  "#1e90ff",
  "#32cd32",
  "#ff1493",
  "#8a2be2",
  "#ff8c00",
  "#00ced1",
  "#dc143c",
];

export default function SettingSidebar({ onPlot }: SettingSidebarProps) {
  const [date, setDate] = useState("");
  const [timezone, setTimezone] = useState("Asia/Tokyo");
  const [site, setSite] = useState("omu1p85m");
  const [targets, setTargets] = useState<Target[]>(INITIAL_TARGETS);
  const [newName, setNewName] = useState("");
  const [newColor, setNewColor] = useState(COLOR_PALETTE[0]);

  const addTargetHandler = () => {
    if (!newName.trim()) return;
    if (
      targets.some(
        (target) => target.name.toLowerCase() === newName.trim().toLowerCase()
      )
    ) {
      toast.error(`Target "${newName}" already exists.`);
      return;
    }

    const usedColors = new Set(targets.map((t) => t.color));
    const colorToSet =
      newColor || COLOR_PALETTE.find((c) => !usedColors.has(c)) || "#000000";

    const newTargets = [...targets, { name: newName, color: colorToSet }];
    setTargets(newTargets);
    setNewName("");

    const currentTargetColors = new Set(newTargets.map((t) => t.color));
    setNewColor(
      COLOR_PALETTE.find((c) => !currentTargetColors.has(c)) || COLOR_PALETTE[0]
    );
  };

  const removeTargetHandler = (index: number) => {
    const updatedTargets = targets.filter((_, i) => i !== index);
    setTargets(updatedTargets);

    const currentTargetColors = new Set(updatedTargets.map((t) => t.color));
    setNewColor(
      COLOR_PALETTE.find((c) => !currentTargetColors.has(c)) || COLOR_PALETTE[0]
    );
  };

  const handlePlot = async () => {
    const payload = { date, timezone, site, targets };
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (!res.ok) {
        if (data.errors && data.errors.length > 0) {
          data.errors.forEach((err: TargetNameError) => {
            toast.error(`Error for ${err.name}: ${err.error}`);
          });
        } else {
          toast.error(data.detail || "Plot Request Failed");
        }
        onPlot(data.imageData ? `data:image/png;base64,${data.imageData}` : "");
        if (data.errors && data.errors.length > 0) {
          const errorNames = new Set(
            data.errors.map((err: TargetNameError) => err.name)
          );
          setTargets((prevTargets) =>
            prevTargets.filter((target) => !errorNames.has(target.name))
          );
        }
        return;
      }

      if (data.imageData) {
        const imageUrl = `data:image/png;base64,${data.imageData}`;
        onPlot(imageUrl);
      } else {
        onPlot("");
      }

      if (data.errors && data.errors.length > 0) {
        data.errors.forEach((err: TargetNameError) => {
          toast.error(`Error for ${err.name}: ${err.error}`);
        });
        const errorNames = new Set(
          data.errors.map((err: TargetNameError) => err.name)
        );
        setTargets((prevTargets) =>
          prevTargets.filter((target) => !errorNames.has(target.name))
        );
      }
    } catch (error) {
      console.error("Plot error (catch block):", error);
      onPlot("");
      toast.error("Network Error: Failed to fetch plot data.");
    }
  };

  useEffect(() => {
    const today = new Date().toISOString().split("T")[0];
    setDate(today);
  }, []);

  useEffect(() => {
    if (targets.length === 0 && COLOR_PALETTE.length > 0) {
      setNewColor(COLOR_PALETTE[0]);
    } else {
      const currentTargetColors = new Set(targets.map((t) => t.color));
      if (!currentTargetColors.has(COLOR_PALETTE[0])) {
        const nextColor =
          COLOR_PALETTE.find((c) => !currentTargetColors.has(c)) ||
          COLOR_PALETTE[0];
        if (newColor !== nextColor) {
          setNewColor(nextColor);
        }
      }
    }
  }, [targets, handlePlot]);

  useEffect(() => {
    if (targets.length > 0 && date && timezone && site) {
      handlePlot();
    }
  }, [targets, date, timezone, site]);

  return (
    <div className="flex flex-col justify-between h-full p-4 space-y-4 overflow-y-auto">
      <ObservationSettings
        date={date}
        setDate={setDate}
        timezone={timezone}
        setTimezone={setTimezone}
        site={site}
        setSite={setSite}
      />
      <TargetList targets={targets} removeTarget={removeTargetHandler} />
      <AddTargetForm
        newName={newName}
        setNewName={setNewName}
        newColor={newColor}
        setNewColor={setNewColor}
        addTarget={addTargetHandler}
      />
    </div>
  );
}

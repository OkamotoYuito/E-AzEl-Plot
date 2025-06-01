"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface AddTargetFormProps {
  newName: string;
  setNewName: (name: string) => void;
  newColor: string;
  setNewColor: (color: string) => void;
  addTarget: () => void;
}

export default function AddTargetForm({
  newName,
  setNewName,
  newColor,
  setNewColor,
  addTarget,
}: AddTargetFormProps) {
  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      addTarget();
    }
  };

  return (
    <div className="space-y-2 pt-4 border-t">
      <div className="space-y-1">
        <Label htmlFor="target-name">Target name</Label>
        <Input
          id="target-name"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="e.g. Moon"
        />
      </div>
      <div className="flex items-center gap-2">
        <Button
          onClick={addTarget}
          className="flex-grow text-sm font-semibold h-9"
        >
          Add Target
        </Button>
        <label className="relative w-8 h-8 cursor-pointer">
          <div
            className="w-full h-full rounded-full border border-input"
            style={{ backgroundColor: newColor }}
          />
          <Input
            type="color"
            value={newColor}
            onChange={(e) => setNewColor(e.target.value)}
            className="absolute inset-0 opacity-0 w-full h-full cursor-pointer"
          />
        </label>
      </div>
    </div>
  );
}

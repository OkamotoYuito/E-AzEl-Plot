"use client";

import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Trash2 } from "lucide-react";

interface Target {
  name: string;
  color: string;
}

interface TargetListProps {
  targets: Target[];
  removeTarget: (index: number) => void;
}

export default function TargetList({ targets, removeTarget }: TargetListProps) {
  return (
    <div className="flex-1 overflow-y-auto space-y-1 pt-4 min-h-[150px]">
      <h3 className="text-base font-semibold px-1">Targets</h3>
      <Separator />
      {targets.map((t, i) => (
        <div
          key={i}
          className="flex justify-between items-center p-1.5 rounded-md hover:bg-muted text-sm"
        >
          <div className="flex items-center gap-1.5">
            <div
              className="w-3 h-3 rounded-full border border-foreground/50"
              style={{ backgroundColor: t.color }}
            />
            <span className="truncate max-w-[180px]">{t.name}</span>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => removeTarget(i)}
            className="h-6 w-6"
          >
            <Trash2 className="h-3 w-3" />
          </Button>
        </div>
      ))}
      {targets.length === 0 && (
        <p className="text-xs text-muted-foreground text-center py-4">
          No targets added.
        </p>
      )}
    </div>
  );
}

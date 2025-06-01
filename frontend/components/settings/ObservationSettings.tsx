"use client";

import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface ObservationSettingsProps {
  date: string;
  setDate: (date: string) => void;
  timezone: string;
  setTimezone: (timezone: string) => void;
  site: string;
  setSite: (site: string) => void;
}

export default function ObservationSettings({
  date,
  setDate,
  timezone,
  setTimezone,
  site,
  setSite,
}: ObservationSettingsProps) {
  return (
    <div className="space-y-4">
      <div className="space-y-1">
        <Label htmlFor="date">Date</Label>
        <Input
          id="date"
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="text-sm"
        />
      </div>
      <div className="space-y-1">
        <Label htmlFor="timezone">Timezone</Label>
        <Select value={timezone} onValueChange={setTimezone}>
          <SelectTrigger id="timezone" className="text-sm">
            <SelectValue placeholder="Select timezone" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="Asia/Tokyo">Asia/Tokyo</SelectItem>
            <SelectItem value="America/New_York">America/New_York</SelectItem>
            <SelectItem value="Europe/London">Europe/London</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-1">
        <Label htmlFor="telescope">Telescope</Label>
        <Select value={site} onValueChange={setSite}>
          <SelectTrigger id="telescope" className="text-sm">
            <SelectValue placeholder="Select telescope" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="omu1p85m">1.85m Telescope</SelectItem>
            <SelectItem value="nanten2">NANTEN2</SelectItem>
            <SelectItem value="nro45">NRO 45m Telescope</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>
  );
}

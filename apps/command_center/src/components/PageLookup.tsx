import { useState } from "react";
import { ContextIdPickers } from "./ContextIdPickers";

type LookupFields = {
  plant?: boolean;
  asset?: boolean;
  alert?: boolean;
  tag?: boolean;
};

export function PageLookup({
  fields = { plant: true, asset: true, alert: true },
  onSearch,
}: {
  fields?: LookupFields;
  onSearch?: (values: { plantId: string; assetId: string; alertId: string; tagId?: string }) => void;
}) {
  const [tag, setTag] = useState("");

  return (
    <div className="lookup-bar">
      <ContextIdPickers
        fields={{ plant: fields.plant, asset: fields.asset, alert: fields.alert }}
        onSearch={(values) => onSearch?.({ ...values, tagId: tag.trim() || undefined })}
      />
      {fields.tag && (
        <label>
          Tag ID
          <input
            value={tag}
            onChange={(e) => setTag(e.target.value)}
            placeholder="PLT-01-U03_TEMP"
          />
        </label>
      )}
    </div>
  );
}

import { type File_extension } from './FileExtension.ts';
import { type Project } from './Projects';

export class StructureCheck {
    constructor(
        public id: string,
        public name: string,
        public obligated_extensions: File_extension[] = [],
        public blocked_extensions: File_extension[] = [],
        public project: Project | null = null,
    ) {}

    /**
     * Convert a structureCheck object to a structureCheck instance.
     *
     * @param structureCheck
     */
    static fromJSON(structureCheck: StructureCheck): StructureCheck {
        return new StructureCheck(structureCheck.id, structureCheck.name);
    }
}

import { type File_extension } from './FileExtension.ts'
import { type Project } from './Projects'

export class StructureCheck {
    constructor(
        public id: string,
        public name: string,
        public obligated_extensions: File_extension[] = [],
        public blocked_extensions: File_extension[] = [],
        public project: Project | null = null
    ) {}

    /**
     * Convert a structure_check object to a structure_check instance.
     *
     * @param structure_check
     */
    static fromJSON(structure_check: StructureCheck): StructureCheck {
        return new StructureCheck(structure_check.id, structure_check.name)
    }
}

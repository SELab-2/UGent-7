import { FileExtension } from './FileExtension.ts';
import { Project } from './Project.ts';

export class StructureCheck {
    constructor(
        public id: string = '',
        public path: string = '',
        public obligated_extensions: FileExtension[] = [],
        public blocked_extensions: FileExtension[] = [],
        public project: Project = new Project(),
    ) {}

    /**
     * Get the directory hierarchy list of this structure check.
     *
     * @return string[] the directory hierarchy.
     */
    public getDirectoryHierarchy(): string[] {
        return this.path.split('/');
    }

    /**
     * Check whether the check exists.
     */
    public exists(): boolean {
        return !!this.id;
    }

    /**
     * Convert a structureCheck object to a structureCheck instance.
     *
     * @param structureCheck
     */
    static fromJSON(structureCheck: StructureCheck): StructureCheck {
        return new StructureCheck(
            structureCheck.id,
            structureCheck.path,
            structureCheck.obligated_extensions.map((extension) => FileExtension.fromJSON(extension)),
            structureCheck.blocked_extensions.map((extension) => FileExtension.fromJSON(extension)),
            Project.fromJSON(structureCheck.project),
        );
    }
}

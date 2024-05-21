import { FileExtension, FileExtensionJSON } from './FileExtension.ts';
import { Project } from './Project.ts';
import { HyperlinkedRelation } from '@/types/ApiResponse.ts';

export type StructureCheckJSON = {
    id: string;
    path: string;
    project: HyperlinkedRelation;
    obligated_extensions: FileExtensionJSON[];
    blocked_extensions: FileExtensionJSON[];
}

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
     * Get the obligated extension list of this structure check.
     *
     * @return string[] the obligated extensions.
     */
    public getBlockedExtensionList(): string[] {
        if (this.blocked_extensions === null) {
            return [];
        }

        return this.blocked_extensions.map((extension) => extension.extension);
    }

    /**
     * Get the blocked extension list of this structure check.
     *
     * @return string[] the blocked extensions.
     */
    public getObligatedExtensionList(): string[] {
        if (this.obligated_extensions === null) {
            return [];
        }

        return this.obligated_extensions.map((extension) => extension.extension);
    }

    /**
     * Set the obligated extension list of this structure check.
     *
     * @param extensions
     */
    public setBlockedExtensionList(extensions: string[]): void {
        this.blocked_extensions = extensions.map((extension) => new FileExtension('', extension));
    }

    /**
     * Set the blocked extension list of this structure check.
     *
     * @param extensions
     */
    public setObligatedExtensionList(extensions: string[]): void {
        this.obligated_extensions = extensions.map((extension) => new FileExtension('', extension));
    }

    /**
     * Set the name of this structure check by updating the last folder in the path.
     *
     * @param folder
     * @param replacement
     */
    public replaceFolderName(folder: string, replacement: string): void {
        // Find the position of the last occurrence
        const lastIndex = this.path.lastIndexOf(folder);

        // If the substring is not found, return
        if (lastIndex === -1) {
            return;
        }

        // Split the string into two parts
        const before = this.path.substring(0, lastIndex);
        const after = this.path.substring(lastIndex + folder.length);

        // Concatenate the parts with the replacement in the middle
        this.path = before + replacement + after;
    }

    /**
     * Set the name of this structure check by updating the last folder in the path.
     *
     * @param name
     */
    public setLastFolderName(name: string): void {
        const path = this.path.split('/');
        path[path.length - 1] = name;
        this.path = path.join('/');
    }

    /**
     * Convert a structureCheck object to a structureCheck instance.
     *
     * @param structureCheck
     */
    static fromJSON(structureCheck: StructureCheckJSON): StructureCheck {
        return new StructureCheck(
            structureCheck.id,
            structureCheck.path,
            structureCheck.obligated_extensions.map(FileExtension.fromJSON),
            structureCheck.blocked_extensions.map(FileExtension.fromJSON),
        );
    }
}

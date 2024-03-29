import { File_extension } from "./FileExtension.ts";
import { Project } from "./Projects";

export class StructureCheck {
    constructor(
        public id: string,
        public name: string,
        public obligated_extensions: File_extension[] = [],
        public blocked_extensions: File_extension[] = [],
        public project: Project = new Project(
            "0",
            "default",
            "this is a default project given in the service because it isnt initiated",
            false,
            true,
            true,
            new Date(),
            new Date(),
            0,
            false,
            0) // TODO check
    ) {
    }


    /**
     * Convert a structure_check object to a structure_check instance.
     *
     * @param structure_check
     */
    static fromJSON(structure_check: StructureCheck): StructureCheck {
        return new StructureCheck(
            structure_check.id,
            structure_check.name
        )
    }
}
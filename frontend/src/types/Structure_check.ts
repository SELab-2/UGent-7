import { File_extension } from "./File_extensions";
import { Project } from "./Projects";

export class Structure_check {
    constructor(
        public id: number,
        public name: string,
        public obligated_extensions: File_extension[] = [],
        public blocked_extensions: File_extension[] = [],
        public project: Project = new Project(
            0,
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
    static fromJSON(structure_check: Structure_check): Structure_check {
        return new Structure_check(
            structure_check.id,
            structure_check.name
        )
    }
}
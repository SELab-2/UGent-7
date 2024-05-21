import { DockerImage } from './DockerImage';
import { HyperlinkedRelation } from '@/types/ApiResponse.ts';

export type ExtraCheckJSON = {
    id: string;
    name: string;
    file: string;
    time_limit: number;
    memory_limit: number;
    show_log: boolean;
    show_artifact: boolean;
    project: HyperlinkedRelation;
    docker_image: HyperlinkedRelation;
}

export class ExtraCheck {
    constructor(
        public id: string = '',
        public name: string = '',
        public file: File | string = '',
        public time_limit: number = 30,
        public memory_limit: number = 128,
        public show_log: boolean = true,
        public docker_image: DockerImage = new DockerImage()
    ) {}

    /**
     * Convert an extra check object to a extraCheck instance.
     *
     * @param extraCheck
     */
    static fromJSON(extraCheck: ExtraCheckJSON): ExtraCheck {
        return new ExtraCheck(
            extraCheck.id,
            extraCheck.name,
            extraCheck.file,
            extraCheck.time_limit,
            extraCheck.memory_limit,
            extraCheck.show_log,
        );
    }
}

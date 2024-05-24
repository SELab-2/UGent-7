export interface DockerImageJSON {
    id: string;
    name: string;
    file: string;
    public: boolean;
    owner: string;
}

export class DockerImage {
    public public: boolean;
    constructor(
        public id: string = '',
        public name: string = '',
        public file: string = '', // in the form of a uri
        public publicStatus: boolean = false,
        public owner: string = '',
    ) {
        this.public = publicStatus;
    }

    static fromJSON(dockerData: DockerImageJSON): DockerImage {
        return new DockerImage(dockerData.id, dockerData.name, dockerData.file, dockerData.public, dockerData.owner);
    }

    static blankDockerImage(): DockerImage {
        return new DockerImage('', '', '', false, '');
    }
}

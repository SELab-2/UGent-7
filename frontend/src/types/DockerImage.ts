export class DockerImage {
    public public: boolean;
    constructor(
        public id: string,
        public name: string,
        public file: string, // in the form of a uri
        public publicStatus: boolean,
        public owner: string,
    ) {
        this.public = publicStatus;
    }

    static fromJSON(dockerData: DockerImage): DockerImage {
        return new DockerImage(dockerData.id, dockerData.name, dockerData.file, dockerData.public, dockerData.owner);
    }

    static blankDockerImage(): DockerImage {
        return new DockerImage('', '', '', false, '');
    }
}

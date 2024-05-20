export enum ErrorMessageEnum {
    // Structure checks errors
    BLOCKED_EXTENSION = 'views.submissions.error.blocked extension',
    OBLIGATED_EXTENSION_NOT_FOUND = 'views.submissions.error.obligatedExtensionNotFound',
    FILE_DIR_NOT_FOUND = 'views.submissions.error.fileDirNotFound',

    // Extra checks errors
    DOCKER_IMAGE_ERROR = 'views.submissions.error.dockerImageError',
    TIME_LIMIT = 'views.submissions.error.timeLimit',
    MEMORY_LIMIT = 'views.submissions.error.memoryLimit',
    CHECK_ERROR = 'views.submissions.error.checkError',
    RUNTIME_ERROR = 'views.submissions.error.runtimeError',
    UNKNOWN = 'views.submissions.error.unknown',
    FAILED_STRUCTURE_CHECK = 'views.submissions.error.failedStructureCheck',
}

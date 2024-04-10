export type GlobModule = {
    default: any;
}

export type GlobState = {
    getRandomImport: () => any;
    getImport: (key: string) => any;
}

export function useGlob(glob: Record<string, GlobModule>): GlobState {
    /**
     * Get a random import from the glob.
     *
     * @returns A random import from the glob.
     */
    function getRandomImport(): any {
        const keys = Object.keys(glob);
        const randomKey = keys[Math.floor(Math.random() * keys.length)];
        return glob[randomKey].default;
    }

    /**
     * Get an import from the glob.
     *
     * @param key
     */
    function getImport(key: string): any {
        if (key in glob) {
            return glob[key].default;
        }

        return Object.values(glob).find((module) => {
            const parts = module.default.split('/');
            return parts[parts.length - 1] === key;
        })?.default;
    }

    return {
        getRandomImport, getImport
    }
}
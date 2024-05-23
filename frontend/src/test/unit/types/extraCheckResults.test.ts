import { describe, it, expect } from 'vitest';

import { ExtraCheckResult } from '@/types/submission/ExtraCheckResult';
import { extraCheckResultData } from './data';
import { createExtraCheckResult } from './helper';

describe('extraCheckResult type', () => {
    it('create instance of extraCheckResult with correct properties', () => {
        const extraCheckResult = createExtraCheckResult(extraCheckResultData);

        expect(extraCheckResult).toBeInstanceOf(ExtraCheckResult);
        expect(extraCheckResult.id).toBe(extraCheckResultData.id);
        expect(extraCheckResult.result).toBe(extraCheckResultData.result);
        expect(extraCheckResult.error_message).toBe(extraCheckResultData.error_message);
        expect(extraCheckResult.log_file).toStrictEqual(extraCheckResultData.log_file);
        expect(extraCheckResult.submission).toBe(extraCheckResultData.submission);
        expect(extraCheckResult.extra_check).toBe(extraCheckResultData.extra_check);
        expect(extraCheckResult.resourcetype).toBe(extraCheckResultData.resourcetype);
    });

    it('create an extraCheckResult instance from JSON data', () => {
        const extraCheckResultJSON = { ...extraCheckResultData };
        const extraCheckResult = ExtraCheckResult.fromJSON(extraCheckResultJSON);

        expect(extraCheckResult).toBeInstanceOf(ExtraCheckResult);
        expect(extraCheckResult.id).toBe(extraCheckResultData.id);
        expect(extraCheckResult.result).toBe(extraCheckResultData.result);
        expect(extraCheckResult.error_message).toBe(extraCheckResultData.error_message);
        expect(extraCheckResult.log_file).toStrictEqual(extraCheckResultData.log_file);
        expect(extraCheckResult.submission).toBe(extraCheckResultData.submission);
        expect(extraCheckResult.extra_check).toBe(extraCheckResultData.extra_check);
        expect(extraCheckResult.resourcetype).toBe(extraCheckResultData.resourcetype);
    });
});
